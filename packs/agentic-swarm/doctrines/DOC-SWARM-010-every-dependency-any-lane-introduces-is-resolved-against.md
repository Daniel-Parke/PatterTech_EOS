---
summary: Every dependency any lane introduces is resolved against the real registry before merge, and an unresolvable name aborts the merge.
type: doctrine
tags: [eos]
id: DOC-SWARM-010
statement: Every dependency any lane introduces is resolved against the real registry before merge, and an unresolvable name aborts the merge.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0477]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:requirements:010]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B10]
---

# DOC-SWARM-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Prevents a fabricated package name entering the trunk. Commercial
models emit non-existent package names at 5.2 per cent or more and
open-source models at 21.7 per cent, across 576,000 samples and 205,474
unique fabricated names (EV-0477). N lanes is N chances,
and an integrator merging lock files without re-resolving launders it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:requirements:010`, lines 219-225, SHA-256 `88c13ab22df014bc1f834b0c8741c07c618b48c5ee805159e34221df1c2750f2`.
