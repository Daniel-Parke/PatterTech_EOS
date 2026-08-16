---
summary: A declared boundary is machine-checked in CI from the first week.
type: doctrine
tags: [eos]
id: DOC-ARCH-001
statement: A declared boundary is machine-checked in CI from the first week.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [has_server_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0146, EV-0147, EV-0148, EV-0154]
review: 2027-02
lifecycle: active
verification_refs: [packs/architecture/CHECKS.md]
migration_sources: [packs/architecture/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-ARCH-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The contract lives in a committed file and a crossing fails the
build. Evidence: import-linter (EV-0147), dependency-cruiser (EV-0148)
and ArchUnit (EV-0146) all show the same thing, that the contract file
makes the intended architecture reviewable rather than folklore.
Prevents: quiet, one-way boundary erosion. MacCormack et al. (EV-0154)
is the mechanism, since structure mirrors the communication structure
that built it, and for a one-person or agent-run codebase the untreated
prediction is a single tightly coupled artefact. The ADR-0008 audit kept
this one binding on a close call: erosion is genuinely hard to reverse,
which is the test, and EV-0154 is peer-reviewed empirical evidence for
the mechanism. What it is not is evidence that the intervention works in
a codebase this small, and the open questions below say so. If the audit
runs again, this is the rule most likely to move.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/architecture/PACK.md:requirements:001`, lines 99-112, SHA-256 `8d65be4ed6cab45b52b69543fd8aaf214cce90a81ba71409e14b402ac80ef546`.
