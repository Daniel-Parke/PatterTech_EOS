---
summary: An experiment fixes its stopping rule, metric, segmentation and sample before data arrives.
type: doctrine
tags: [eos]
id: DOC-DISC-002
statement: An experiment fixes its stopping rule, metric, segmentation and sample before data arrives.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [runs_experiment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0059, EV-0406]
review: 2028-06
lifecycle: active
verification_refs: [packs/product-discovery/CHECKS.md]
migration_sources: [packs/product-discovery/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-DISC-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`runs_experiment`. All four are written
in the record before the change ships. Prevents the practices that are
wrong by construction, chiefly stopping at first significance and
reading small-sample results as directional
(`EV-0406`), and matches the asymmetric gate where
goal metrics drive the ship decision and guardrails block only on
significant harm (EV-0059). Basis: empirical-evidence.

Activation gives advice, never permission. Nothing here lowers a tier
floor in `kernel/POLICY_SPEC.md` or converts a manual-only action class
into an autonomous one under `kernel/GUARD_SPEC.md`. A BUILD verdict is
not an approval to ship.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/product-discovery/PACK.md:requirements:002`, lines 119-131, SHA-256 `6dfe07a658cf693ba47ff5debb6f21c5d123a1d1deb7dac12870639620674b6d`.
