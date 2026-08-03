---
summary: Where module boundaries live, whether convention, a machine contract, the directory tree, or a runtime call graph
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0146, EV-0147, EV-0148, EV-0154, EV-0159]
review: 2026-12
type: guide
tags: [arch, tooling, ci]
review_by: 2026-12
---

# WG-ARCH-001: where do module boundaries live?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. The fork survives unchanged; the grading of
its output moved from binding-by-assertion to binding on B1 of
`packs/architecture/PACK.md`, which requires the check, not the shape.

## The question

Every codebase claims a layering. The fork is what stops it eroding: a
convention people remember, a machine-checked import contract, a
directory tree that makes violations physically awkward, or a runtime
call graph that sees what static analysis cannot. Erosion is quiet and
one-way. By the time a boundary hurts, it has been crossed for months.

## It depends on

- Who writes the code. Agents cross conventions without noticing and
  respect failing checks absolutely.
- Whether a proof of harmless movement exists, so re-shaping the tree
  is safe.
- How many consumers a shared layer has.
- How much of the wiring is dynamic: reflection, dependency injection,
  service locators, string-keyed lookup.

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

## Decision rule

Agents writing the code, or a second consumer of any shared layer:
at least **B**, from the first week, and B is binding under B1 of the
pack. Move to **C** once a canary exists proving moves are
output-neutral, and do it in one reviewed change. Add **D** only when
dynamic wiring is load-bearing and has already caused an incident.
**A** alone is acceptable only for a single-surface venture with no
agent writing code, which in this estate means almost never.

## Default

**B**, rising to **C** once a canary exists.

## Worked rulings

- **PatterTech_Business (2026-06, argued)**: B first, rings enforced
  by import-linter over a flat tree; then C once an output-hash canary
  proved the physical move neutral, with both hashes unchanged after
  the re-shape.
- **WiseWattage (2026, argued)**: B in substance. One-way dependencies
  from app to api to engine, documented and review-enforced, with CI
  boundary checks arriving piecemeal. The erosion it suffered first is
  why the rule exists.
- **Venture A (2026-07, inherited)**: B taken from the estate default
  at inception, no separate argument recorded.

## Counter-evidence

Every static tool in the ledger states the same blind spot in its own
documentation (EV-0146, EV-0147, EV-0148), so B is a partial check
that is being asked to carry a binding rule. Shopify's answer to that
gap is not available to us. No source measures whether enforced
boundaries improve outcomes in a codebase of this size; the rule
stands on the erosion mechanism and on three ventures' experience of
what happens without it.
