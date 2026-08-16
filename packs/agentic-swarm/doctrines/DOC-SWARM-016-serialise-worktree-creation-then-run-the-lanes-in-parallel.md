---
summary: Serialise worktree creation, then run the lanes in parallel.
type: doctrine
tags: [eos]
id: DOC-SWARM-016
statement: Serialise worktree creation, then run the lanes in parallel.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [fans_work_across_lanes]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0460, EV-0464]
review: on-change-of:agent-harness-major-release
lifecycle: active
verification_refs: [packs/agentic-swarm/CHECKS.md]
migration_sources: [packs/agentic-swarm/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-SWARM-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

and
provision each worktree with the ignored configuration it needs to
verify itself. Three or more concurrent creations race on the git config
lock, killing agents before they start (EV-0464); a worktree without its
environment hands you work the lane could not check (EV-0460).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/agentic-swarm/PACK.md:defaults:006`, lines 262-266, SHA-256 `13719c5b047d2993fc39d91a5dbd0775e5068229cd64b44c4cb1a3e4f2799497`.
