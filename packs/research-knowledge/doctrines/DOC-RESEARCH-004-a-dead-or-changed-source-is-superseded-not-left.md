---
summary: A dead or changed source is superseded, not left.
type: doctrine
tags: [eos]
id: DOC-RESEARCH-004
statement: A dead or changed source is superseded, not left.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [supersedes_a_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0541, EV-0542]
review: 2029-08
lifecycle: active
verification_refs: [packs/research-knowledge/CHECKS.md]
migration_sources: [packs/research-knowledge/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-RESEARCH-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

When a source
stops resolving, moves, or ships a version that changes what it says,
the record records which of the three happened, and every claim resting
on it is re-ruled as still standing, narrowed, or withdrawn. A copy is
frozen at first read, so the claim can be checked when the live page
cannot (EV-0541 separates link rot from content drift; EV-0542 is how a
frozen state is addressed rather than remembered). Predicate:
`supersedes_a_source`. Prevents: a knowledge base whose claims are true
of a world that has moved, which is worse than an empty one because it
reads as current.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/research-knowledge/PACK.md:requirements:004`, lines 155-164, SHA-256 `55e16981c4733455dc9d2f2bafb8fa30226d8b4187f96bc639f7320241b88750`.
