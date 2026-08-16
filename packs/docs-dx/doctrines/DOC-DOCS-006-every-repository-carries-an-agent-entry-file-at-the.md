---
summary: Every repository carries an agent entry file at the conventional root path, and the commands it names are covered by B3.
type: doctrine
tags: [eos]
id: DOC-DOCS-006
statement: Every repository carries an agent entry file at the conventional root path, and the commands it names are covered by B3.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0044]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-DOCS-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The
convention fixes location and nothing else, which is why it was adopted
across vendors that agree on very little (EV-0044). Reason: an agent
guessing at build and test commands, and the softer failure where the
file exists, is never checked, and confidently names a command removed
two releases ago. Adoption counts measure file existence, so presence
alone is worth nothing without the second half. Authority: default.
Basis: decision.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:requirements:006`, lines 184-192, SHA-256 `13075791146c745d0b648b64dd7481708af4ef0a1e1a72f9435c72d6c58ee79b`.
