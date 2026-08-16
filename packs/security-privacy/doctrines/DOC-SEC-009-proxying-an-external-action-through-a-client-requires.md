---
summary: Proxying an external action through a client requires consent for that client.
type: doctrine
tags: [eos]
id: DOC-SEC-009
statement: Proxying an external action through a client requires consent for that client.
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

# DOC-SEC-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Predicate: `has_external_egress` or `runs_agents`. Prevents: an irreversible action taken on the strength of a sentence someone typed. Two boundary MUSTs ride with B6 where the venture speaks MCP or publishes tools: no token passthrough, no session identifier used as authentication, per-client consent before proxying, and the exact command shown before any local installation (EV-0011, EV-0218).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:requirements:006`, lines 153-165, SHA-256 `580355690510bf14b9ce397ef23eb63aed546588fee10c9cbca98edb6ba64cc2`.
