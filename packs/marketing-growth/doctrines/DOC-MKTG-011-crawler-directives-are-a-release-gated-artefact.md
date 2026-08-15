---
summary: Crawler directives are a release-gated artefact.
type: doctrine
tags: [eos]
id: DOC-MKTG-011
statement: Crawler directives are a release-gated artefact.
kind: doctrine
authority: default
basis: law
evidence_grade: observational
scope: estate
applies_when: [publishes_public_content]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0358]
review: on-change-of:PECR-reg-22-amendment
lifecycle: active
verification_refs: [packs/marketing-growth/CHECKS.md]
migration_sources: [packs/marketing-growth/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-MKTG-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The robots
file ships through the same pipeline as code, with a test asserting the
production profile carries no blanket disallow and a staging fixture
that fails the same test. Reason: a 5xx on that file means a conforming
crawler must assume complete disallow (EV-0358), so a botched
deploy is a self-inflicted deindexing incident. It is not a security
control and never names a secret path.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/marketing-growth/PACK.md:defaults:008`, lines 206-212, SHA-256 `c8df303e5b3096dd11d2910b63f5d69e1243ab653b4cd02bfe46ff6da90813c7`.
