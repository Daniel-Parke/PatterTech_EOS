---
summary: Background jobs run on a durable database claim queue.
type: doctrine
tags: [eos]
id: DOC-ARCH-009
statement: Background jobs run on a durable database claim queue.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0157]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-ARCH-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reason:
one store, exactly the database's guarantees, and jobs survive a deploy.
Argued at `packs/architecture/wargames/WG-ARCH-004-job-execution.md`.
Where a state change must also produce a message, use an outbox in the
same transaction and make every consumer idempotent (EV-0157).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:006`, lines 175-179, SHA-256 `2fafdb84cbcd9f585b7ba0c41629138a36cef0d963b9925ad3b243139228aa49`.
