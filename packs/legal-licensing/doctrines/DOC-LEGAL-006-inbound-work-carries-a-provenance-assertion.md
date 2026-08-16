---
summary: Inbound work carries a provenance assertion.
type: doctrine
tags: [eos]
id: DOC-LEGAL-006
statement: Inbound work carries a provenance assertion.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [accepts_contribution]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0345, EV-0352]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-LEGAL-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`accepts_contribution`. One sign-off line per commit, in the form the
certification defines, a real name and a reachable address, checked by
a hook (EV-0345). Agent-written commits are included, because
authorship of machine output is unsettled and provenance is the part we
can record (EV-0352). Reason: code of unknown origin becomes
load-bearing before anyone asks where it came from, and the history is
the only place the answer keeps. Depart where every contributor is
covered by an engagement that already grants the rights, and record
that in the lock-book. Authority: default, because the estate ruled
this and no source compares the alternatives on outcomes; see the open
question about contributor agreements below. Basis: decision.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:requirements:006`, lines 206-217, SHA-256 `0ab508cfa71d6b05ac5935b4d753022f8555239f75b137c6db6164b44a15abf9`.
