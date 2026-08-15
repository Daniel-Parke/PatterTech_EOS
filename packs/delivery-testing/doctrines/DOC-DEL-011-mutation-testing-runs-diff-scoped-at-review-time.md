---
summary: Mutation testing runs diff-scoped at review time.
type: doctrine
tags: [eos]
id: DOC-DEL-011
statement: Mutation testing runs diff-scoped at review time.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0019, EV-0191, EV-0192]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

with the
  conditional, relational and statement-deletion operators, not
  full-repo per commit (EV-0192, EV-0019, EV-0191). Reason: whole-repo
  runs cost more than they return, and coupling to real faults is
  concentrated in a few operators.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:defaults:006`, lines 241-245, SHA-256 `f3ad2c5251f156ea1b960ce87a412fa577560e57acdaf1181233587eae71648b`.
