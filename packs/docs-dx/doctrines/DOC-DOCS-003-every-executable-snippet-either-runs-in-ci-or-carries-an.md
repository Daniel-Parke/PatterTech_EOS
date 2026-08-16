---
summary: Every executable snippet either runs in CI or carries an explicit declaration of why it does not.
type: doctrine
tags: [eos]
id: DOC-DOCS-003
statement: Every executable snippet either runs in CI or carries an explicit declaration of why it does not.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0330]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-DOCS-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A fenced block that names a command,
flag or API call is executed by the documentation gate, or it carries a
marker saying it is illustrative, environment-bound or expected to
fail. Absence of the marker is itself the finding (EV-0330). Reason:
the drifted quickstart. A flag is renamed, the shell block in the
quickstart still names the old spelling, and nothing anywhere knows.
Depart where nothing in the tree can execute the block, and record
which blocks that covers. Authority: default. Basis: standard, from a
toolchain that has run this way for a decade. Scope note: executing a
snippet proves it runs, never that it is the right snippet to show, and
the prose around it stays unverified. See
`packs/docs-dx/wargames/WG-DOCS-002-executable-examples.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:requirements:003`, lines 141-153, SHA-256 `bb957fe0910694fb98ce7260b728aacc0b45f966abb74f9e7ca530d638ba942a`.
