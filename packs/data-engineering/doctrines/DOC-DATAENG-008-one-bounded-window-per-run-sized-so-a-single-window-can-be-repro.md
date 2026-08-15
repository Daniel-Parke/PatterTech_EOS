---
summary: One bounded window per run, sized so a single window can be reprocessed inside the schedule interval.
type: doctrine
tags: [eos]
id: DOC-DATAENG-008
statement: One bounded window per run, sized so a single window can be reprocessed inside the schedule interval.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ingests_external_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0505, EV-0506, EV-0507, EV-0508, EV-0509, EV-0510, EV-0511, EV-0512, EV-0513, EV-0514, EV-0515, EV-0516]
review: 2028-04
lifecycle: active
verification_refs: [packs/data-engineering/CHECKS.md]
migration_sources: [packs/data-engineering/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D5]
---

# DOC-DATAENG-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

If a day's window takes
thirty hours to rerun, the window is wrong, and the pipeline has no
recovery path that does not fall further behind.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-engineering/PACK.md:defaults:005`, lines 221-224, SHA-256 `13543f077e5902fc3bc2b72b5e4a77af24e07fcd7d954d0b26b4d25c3bc75608`.
