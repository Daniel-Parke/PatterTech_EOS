---
summary: Claims about people that a model produced are labelled unverified.
type: doctrine
tags: [eos]
id: DOC-DISC-001
statement: Claims about people that a model produced are labelled unverified.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [cites_user_claim]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0413]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-DISC-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`cites_user_claim`. A persona, segment or quotation
generated rather than observed is marked at the point of use, and it
never carries a decision on its own. Prevents the confidently wrong
segment: against two real survey datasets, no tested model beat the
strongest non-LLM baseline at the individual level, and on segment
targeting the models inflated between-segment gaps two to fourfold and
would have pointed a team at the wrong segment in half the US cases
(`EV-0413`). Scope note: that benchmark is
attitudinal survey prediction, not interview simulation or task
observation. Basis: empirical-evidence.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:requirements:001`, lines 107-117, SHA-256 `3f3fc3b0b6462b3f7ead5711ee7f3b4e4c6c08909b7b8b92d5945bbc2ab9bfd4`.
