---
summary: Derived values are computed, not stored.
type: doctrine
tags: [eos]
id: DOC-ARCH-008
statement: Derived values are computed, not stored.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0010, EV-0023, EV-0024, EV-0025, EV-0057, EV-0097, EV-0098, EV-0099, EV-0100, EV-0101, EV-0102, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-ARCH-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The two sanctioned
exceptions are a cache with a named invalidation owner and an immutable
snapshot carrying its input digest. Reason: a stored derivation drifts
from its source silently, and a cache without an owner is a slow bug.
Argued at `packs/architecture/guides/WG-ARCH-003-derived-state.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:defaults:005`, lines 169-173, SHA-256 `25ea6dde696062525dd4f78d9b705ee2eddc14bb03f74c4dc6d1a6b98f1aed42`.
