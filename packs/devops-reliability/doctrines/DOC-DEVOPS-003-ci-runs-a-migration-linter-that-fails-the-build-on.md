---
summary: CI runs a migration linter that fails the build on destructive and backwards-incompatible findings, and the change record names the risk class of every migration in the change.
type: doctrine
tags: [eos]
id: DOC-DEVOPS-003
statement: CI runs a migration linter that fails the build on destructive and backwards-incompatible findings, and the change record names the risk class of every migration in the change.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0202]
review: 2027-04
lifecycle: active
verification_refs: [packs/devops-reliability/CHECKS.md]
migration_sources: [packs/devops-reliability/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEVOPS-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The four classes are
   destructive, backwards-incompatible, data-dependent and non-linear
   history; only the first two are reliably decidable before running, so
   those two fail and the rest warn (EV-0202). *Prevents*: an
   irreversible DDL reaching production because the diff looked small.
   *Basis*: decision, on one analyzer's documented class taxonomy. Binds
   as a production-safety floor.

   **How the contract step gets through this gate.** The contract phase
   requirement 1 mandates is a destructive migration, so this linter is
   built to fail the one step the pack requires. A drill found that the
   pack never said how both hold, and an agent obeying them in order
   stalls at the drop. The route through is evidence, not an override.
   A destructive migration passes only when it declares itself the
   contract phase of a named expand, migrate, contract sequence, names
   the two earlier migrations by id, and names the deploy in which the
   last reader of the old shape went away. The linter fails a
   destructive finding carrying no such declaration, and fails one whose
   named predecessors are not both already deployed. There is no bare
   skip flag, because what makes the drop safe is the sequence, and the
   sequence is a fact CI can check. A drop with nothing behind it is
   the failure this gate is for, and it still fails.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/devops-reliability/PACK.md:requirements:003`, lines 158-181, SHA-256 `f421f9201d37092eb055974fc85064065c9177df1c362e4adb97d3ab76860db0`.
