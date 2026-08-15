---
summary: No lethal trifecta without a named mediating control.
type: doctrine
tags: [eos]
id: DOC-SEC-002
statement: No lethal trifecta without a named mediating control.
kind: doctrine
authority: binding
basis: decision
evidence_grade: observational
scope: estate
applies_when: [runs_agents]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0219, EV-0220]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
accepted_adr: ADR-0012
---

# DOC-SEC-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No agent
context holds private data, untrusted content and outbound network at
the same time unless a written exception names the control that makes
it safe (EV-0219). Filesystem containment and egress containment are
enabled together or neither is claimed; each alone is defeated through
the other's gap (EV-0220). A broad allowlist entry does not satisfy the
third leg: the Claude Code proxy rules on the client-supplied hostname
without inspecting TLS, so allowing a large host leaves the path open
(EV-0220). Predicate: `runs_agents`. Prevents: silent exfiltration.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:requirements:002`, lines 115-123, SHA-256 `bfabf3e8bcd50f0c833e02d9995ca9dc2f5f5448292b59c0bda6b018e4b9ee26`.
