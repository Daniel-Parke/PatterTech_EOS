---
id: WG-ARCH-001
summary: Where module boundaries live, whether convention, a machine contract, the directory tree, or a runtime call graph
kind: wargame
type: wargame
tags: [arch, ci, eos, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-ARCH-001, DOC-ARCH-004, DOC-ARCH-005]
applies_when: [has_server_code]
engages_when: [requires_independent_deployability]
consequence: high
relations: [DREL-ARCH-003]
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0146, EV-0147, EV-0148, EV-0154, EV-0159, EV-0564]
review: 2026-12
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-ARCH-001: where do module boundaries live?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. The fork survives unchanged; the grading of
its output moved from binding-by-assertion to binding on B1 of
`packs/architecture/PACK.md`, which requires the check, not the shape.

## Decision question and stakes

Every codebase claims a layering. The fork is what stops it eroding: a
convention people remember, a machine-checked import contract, a
directory tree that makes violations physically awkward, or a runtime
call graph that sees what static analysis cannot. Erosion is quiet and
one-way. By the time a boundary hurts, it has been crossed for months.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-001` (binding): A declared boundary is machine-checked in CI from the first week.
- `DOC-ARCH-004` (default): One deployable, one database, modules enforced in the build.
- `DOC-ARCH-005` (default): Split only on a measured signal, never on a label.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Who writes the code. Agents cross conventions without noticing and
  respect failing checks absolutely.
- Whether a proof of harmless movement exists, so re-shaping the tree
  is safe.
- How many consumers a shared layer has.
- How much of the wiring is dynamic: reflection, dependency injection,
  service locators, string-keyed lookup.

Applicability is `has_server_code`. Engagement is `requires_independent_deployability`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Convention

**What it is.** A documented layering enforced by review.

**Buys.** Nothing to install, nothing to maintain, no false positives.

**Costs.** It erodes at the speed of the busiest week. MacCormack et
al. (EV-0154) supply the mechanism: structure mirrors the
communication structure that produced it, and for a solo or agent-run
codebase the untreated prediction is one tightly coupled artefact.

### B. Machine contract over any layout

**What it is.** A contract file in CI. import-linter for Python
(EV-0147) with its three shapes, layers, forbidden and independence;
dependency-cruiser for TypeScript (EV-0148); ArchUnit for the JVM
(EV-0146), where the rules are ordinary unit tests.

**Buys.** A red build on a crossing, wherever the files sit, and a
contract file that is itself the reviewable statement of the
architecture.

**Costs.** Static imports only. Dynamic wiring is invisible. The
contract file must be kept in step with package renames by hand, and
it says nothing about whether the decomposition is any good.

### C. The tree is the architecture

**What it is.** Boundaries as physical directories, plus the machine
contract. The location of a file answers whether an import is allowed.

**Buys.** A violation looks wrong before any tool runs, which is the
cheapest possible review.

**Costs.** The move itself. Only safe with a behaviour canary proving
it changed nothing, and it needs doing in one reviewed change.

### D. Runtime call graph

**What it is.** Call graphs captured from CI runs, scored per
component. Shopify's approach (EV-0159).

**Buys.** The dynamic violations B cannot see.

**Costs.** The tool is in-house and not public. It needs
representative CI coverage to mean anything, and it usually arrives as
a score that tolerates violations rather than a gate that blocks them,
which is a migration tactic for legacy mass, not a greenfield rule.

## Failure premises

### Premortem for A. Convention

Assume `A. Convention` was selected and the outcome failed. Test this option's stated failure mechanism first: It erodes at the speed of the busiest week. MacCormack et al. (EV-0154) supply the mechanism: structure mirrors the communication structure that produced it, and for a solo or agent-run codebase the untreated prediction is one tightly coupled artefact.

### Premortem for B. Machine contract over any layout

Assume `B. Machine contract over any layout` was selected and the outcome failed. Test this option's stated failure mechanism first: Static imports only. Dynamic wiring is invisible. The contract file must be kept in step with package renames by hand, and it says nothing about whether the decomposition is any good.

### Premortem for C. The tree is the architecture

Assume `C. The tree is the architecture` was selected and the outcome failed. Test this option's stated failure mechanism first: The move itself. Only safe with a behaviour canary proving it changed nothing, and it needs doing in one reviewed change.

### Premortem for D. Runtime call graph

Assume `D. Runtime call graph` was selected and the outcome failed. Test this option's stated failure mechanism first: The tool is in-house and not public. It needs representative CI coverage to mean anything, and it usually arrives as a score that tolerates violations rather than a gate that blocks them, which is a migration tactic for legacy mass, not a greenfield rule.

## Decision rule

Agents writing the code, or a second consumer of any shared layer:
at least **B**, from the first week, and B is binding under B1 of the
pack. Move to **C** once a canary exists proving moves are
output-neutral, and do it in one reviewed change. Add **D** only when
dynamic wiring is load-bearing and has already caused an incident.
**A** alone is acceptable only for a single-surface venture with no
agent writing code, which in this estate means almost never.

## Safe default

**B**, rising to **C** once a canary exists.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Who writes the code. Agents cross conventions without noticing and respect failing checks absolutely.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** **B**, rising to **C** once a canary exists.

**Exit condition:** Stop or roll back the selected branch when It erodes at the speed of the busiest week. MacCormack et al. (EV-0154) supply the mechanism: structure mirrors the communication structure that produced it, and for a solo or agent-run codebase the untreated prediction is one tightly coupled artefact, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Who writes the code. Agents cross conventions without noticing and respect failing checks absolutely.

## Counter-evidence and transfer limits

Every static tool in the ledger states the same blind spot in its own
documentation (EV-0146, EV-0147, EV-0148), so B is a partial check
that is being asked to carry a binding rule. Shopify's answer to that
gap is not available to us. No source measures whether enforced
boundaries improve outcomes in a codebase of this size; the rule
stands on the erosion mechanism and on three ventures' experience of
what happens without it.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
