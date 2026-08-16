---
summary: Online-first with a read cache, until an offline write is a named requirement.
type: doctrine
tags: [eos]
id: DOC-NAT-009
statement: Online-first with a read cache, until an offline write is a named requirement.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0382]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-NAT-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason: no local writes means no conflicts and no policy
to maintain, and a serious sync project narrowed itself to the read
path and left writes to the application (EV-0382).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:defaults:002`, lines 210-213, SHA-256 `8861051d650b23675745e027fadb283e12728a1d4b29eb862c9b483c78743fd0`.
