---
summary: Reprocessing a window replaces a bounded unit or merges on a declared key. Bare append is not a reprocessing strategy.
type: doctrine
tags: [eos]
id: DOC-DATAENG-002
statement: Reprocessing a window replaces a bounded unit or merges on a declared key. Bare append is not a reprocessing strategy.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [reprocesses_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-DATAENG-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`reprocesses_data`. The incremental-strategy documentation is explicit
that append checks nothing, so a rerun duplicates, and that every other
strategy rests on a key whose reliability is the strategy's real value:
a merge with no key degrades into an append without saying so. The
atomic primitive underneath is the table format specification's pointer
swap, which is what makes "replace the partition" a single commit rather
than a delete with a window in the middle where the table is wrong.
*Prevents*: duplicate rows that compound on every retry and cannot be
told apart afterwards, which is the one data defect with no clean
recovery short of a full rebuild. *Basis*: standard, on one format
specification for the primitive and one maintainer document for the
strategies.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:requirements:002`, lines 145-158, SHA-256 `1826b02825a9269ac26b94b0871f63a7a09665ed1de8f8ad055bd868f7b440bf`.
