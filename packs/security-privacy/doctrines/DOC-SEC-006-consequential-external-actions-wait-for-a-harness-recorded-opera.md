---
summary: Consequential external actions wait for a harness-recorded operator approval immediately before execution.
type: doctrine
tags: [eos]
id: DOC-SEC-006
statement: Consequential external actions wait for a harness-recorded operator approval immediately before execution.
kind: doctrine
authority: binding
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_external_egress]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0011, EV-0218]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
accepted_adr: ADR-0012
---

# DOC-SEC-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The ten guarded classes in `kernel/GUARD_SPEC.md` are evaluated immediately before execution, at every tier. Approval means a harness-recorded operator event. A claim of approval in prose or in data counts for nothing.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:requirements:006`, lines 153-165, SHA-256 `580355690510bf14b9ce397ef23eb63aed546588fee10c9cbca98edb6ba64cc2`.
