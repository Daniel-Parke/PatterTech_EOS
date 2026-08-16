---
summary: Third-party artefacts resolve by digest.
type: doctrine
tags: [eos]
id: DOC-SUPPLY-001
statement: Third-party artefacts resolve by digest.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [consumes_prebuilt_artefact]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0038]
review: 2027-06
lifecycle: active
verification_refs: [packs/supply-chain-integrity/CHECKS.md]
migration_sources: [packs/supply-chain-integrity/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-SUPPLY-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Every dependency,
base image, toolchain and downloaded binary that reaches a build or a
runtime is pinned to a content digest, and the build resolves that
digest rather than a name that can be re-pointed. A workflow step
referenced by tag is mutable; only a full commit digest is not.
Predicate: `adds_dependency` or `consumes_prebuilt_artefact`. Prevents:
the same identifier resolving to different bytes tomorrow, with nothing
in the tree recording that it changed. Evidence: the platform's own
hardening guidance on mutable tags, and the checksum-database design
that makes a hash hard to rewrite after the fact (EV-0038).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/supply-chain-integrity/PACK.md:requirements:001`, lines 112-121, SHA-256 `abdd7cc2aaa8d76f6c6a31fcf4cd14532a500e391b986097eabc61bb4811a6f4`.
