---
summary: Verification staged by risk and stability.
type: doctrine
tags: [eos]
id: DOC-DEL-008
statement: Verification staged by risk and stability.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0036, EV-0096, EV-0105, EV-0191, EV-0192]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:defaults:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

and this is a default
  set, not law. The floors are the law; the staging is argued. Stages,
  in the order they switch on:

  | Stage | What runs | Switched on by |
  | --- | --- | --- |
  | Risk floors | The acceptance-first row above, plus the guard's runtime floors | Day one, unconditionally |
  | Cheap executable checks | Build, types, lint, schema, smoke | Day one, before the first feature lane opens |
  | Contract tests | The boundary's cases, blocking for its neighbours | The moment that interface is declared stable |
  | Comprehensive harness | Regression breadth, derived from the map and the specifications | When the stability signals below fire |
  | Deletion | Tests that only protect retired structure | The same change that retires the structure |

  Executable is the operative word in the second row. A cheap tier that
  is a list in a document and not a command that exits non-zero buys
  nothing, and requirement 5 is the version of that with teeth.

  The harness is derived from the map and the specifications rather than
  from the code, authored or reviewed independently of the implementing
  agent, and mutation-checked before it blocks anything (EV-0191,
  EV-0192, EV-0105). Default stability signals, and these are starting
  values a venture overrides in its lock-book rather than measured
  thresholds: all journeys green on the acceptance spine, three
  consecutive integrations with no interface churn, and a flat trend in
  open defects over the same window.

  No percentage gates the harness. We found no standard, study or mature
  practice that gates rigour on a completeness figure: the precedents
  gate on consequence class and on measured behaviour, which is what an
  error budget does (EV-0096) and what per-practice maturity does
  (EV-0036). While the harness is deferred, name the deferral at the
  venture's regular review, because deferred breadth is a loan and
  nobody sees the interest until it is due. Reason for the whole staging
  being a default: tests attached to churning internals are rewritten
  with the churn, so deferring breadth is argued rather than proved, and
  the claim that deferral reduces waste without raising escaped defects
  is a hypothesis ADR-0006 labels as one.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:defaults:003`, lines 194-229, SHA-256 `2f983027c78bbb2d59239f6d95f82aac011c141b0f3e104a2f44a8ec6df7e16f`.
