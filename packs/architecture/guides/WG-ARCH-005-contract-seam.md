---
id: WG-ARCH-005
summary: How frontend and backend come to agree on types, whether hand-maintained, generated and gated, one language end to end, or parsed at the edge
kind: wargame
type: wargame
tags: [arch, ci, eos, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-ARCH-002, DOC-ARCH-003]
applies_when: [has_cross_language_contract]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0023, EV-0025, EV-0057, EV-0147, EV-0148, EV-0193, EV-0285]
review: 2027-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-ARCH-005: how do frontend and backend agree on types?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. The gate is now the part that binds, as B4 of
`packs/architecture/PACK.md`, while the choice between options stays a
default. A fourth option arrived too, parsing at the edge, because
generation proves what compiled and nothing about what is running.

## Decision question and stakes

Two codebases describe the same request and the same response. The fork
is what keeps them agreeing: discipline, generation, unification, or
parsing. The failure that decides it is the quiet one, where a renamed
field makes a mutation fail and the interface reports success, and each
option decides when that surfaces.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-002` (binding): Generated contract artefacts are produced deterministically from a committed source and CI fails when they drift.
- `DOC-ARCH-003` (binding): A typed client verifies that a response succeeded before treating the response body as data.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- One language across the seam, or two.
- Whether generation can run offline and deterministically.
- Whether both sides ship from one commit, or drift apart.
- Who else calls the boundary, and whether you can rebuild them.
- Whether the client's model should be the wire shape at all.

Applicability is `has_cross_language_contract`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Hand-maintained client types

**What it is.** The client declares the shapes it needs and a person
keeps them in step.

**Buys.** No build step, and the client models what the interface needs
rather than what the handler returns. The only option left when the
other side publishes no schema.

**Costs.** Nothing fails when the two disagree, so review is the whole
defence, and review is what the busiest week takes away first.

### B. Generated from the schema, committed, drift-gated

**What it is.** The schema is emitted from the API offline and
deterministically (EV-0023), then compiled into a committed types
package and a typed client that checks the response succeeded. CI fails
when the copy lags its source, and import-linter (EV-0147) or
dependency-cruiser (EV-0148) forbids importing around that client.

**Buys.** A backend change the frontend has not absorbed becomes a red
build in the commit that made it.

**Costs.** Build-time agreement only: it proves the client compiled
against a schema, not that the deployed server matches it. The generated
surface is the wire shape. Without a failing check the artefacts rot, a
lesson `registry/LESSONS.md` records from experience.

### C. One language end to end, types shared as source

**What it is.** tRPC-style inference, or a models package both sides
import. No generator and no artefact; the compiler is the contract.

**Buys.** The seam disappears. A rename is a compile error in the same
commit, and there is nothing to keep deterministic and nothing to rot.

**Costs.** Unavailable across Python and TypeScript, which is most of
this estate. It couples release, since shared source is true only while
both sides ship together, so a client on last week's bundle believes a
contract the server dropped, and outsiders get no artefact to read.

### D. Schema at run time, parsed at the edge

**What it is.** One schema artefact describes the wire (EV-0025) and
each side parses what arrives against it, narrowing to a domain type at
the boundary instead of re-checking fields downstream (EV-0285).

**Buys.** The failures B cannot see: a server that no longer matches its
published schema, a proxy dropping a field, a stale client. Each becomes
a located failure with the payload attached, typed language or not.

**Costs.** It fails after deployment, not before, costs something per
request, and needs a designed failure path for unparseable responses.

## Failure premises

### Premortem for A. Hand-maintained client types

Assume `A. Hand-maintained client types` was selected and the outcome failed. Test this option's stated failure mechanism first: Nothing fails when the two disagree, so review is the whole defence, and review is what the busiest week takes away first.

### Premortem for B. Generated from the schema, committed, drift-gated

Assume `B. Generated from the schema, committed, drift-gated` was selected and the outcome failed. Test this option's stated failure mechanism first: Build-time agreement only: it proves the client compiled against a schema, not that the deployed server matches it. The generated surface is the wire shape. Without a failing check the artefacts rot, a lesson `registry/LESSONS.md` records from experience.

### Premortem for C. One language end to end, types shared as source

Assume `C. One language end to end, types shared as source` was selected and the outcome failed. Test this option's stated failure mechanism first: Unavailable across Python and TypeScript, which is most of this estate. It couples release, since shared source is true only while both sides ship together, so a client on last week's bundle believes a contract the server dropped, and outsiders get no artefact to read.

### Premortem for D. Schema at run time, parsed at the edge

Assume `D. Schema at run time, parsed at the edge` was selected and the outcome failed. Test this option's stated failure mechanism first: It fails after deployment, not before, costs something per request, and needs a designed failure path for unparseable responses.

## Decision rule

Two languages across the seam: **B**, always, generation offline and the
artefacts committed. B4 binds the gate, not the choice of option. Add
**D** where the two sides can be deployed apart, or where the other side
is not yours to rebuild, since B fails at build time and D fails at run
time. One language, one repo, one release: **C** is legitimate, gated
the same way for anything leaving the repo. **A** is the ruling only
where the other side publishes no schema. Whichever wins, freeze the
interface and leave the internals alone (EV-0057).

## Safe default

**B**, which is also the seam rule of stack profile 03
(`registry/stacks/STACK-fullstack-app.md`). The estate runs Python
services under TypeScript fronts, so the seam is generated, committed
and gated, or it lies. Where the boundary is public,
`packs/api-integration/PACK.md` rules who authors the contract.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **One language across the seam, or two.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** **B**, which is also the seam rule of stack profile 03 (`registry/stacks/STACK-fullstack-app.md`). The estate runs Python services under TypeScript fronts, so the seam is generated, committed and gated, or it lies. Where the boundary is public, `packs/api-integration/PACK.md` rules who authors the contract.

**Exit condition:** Stop or roll back the selected branch when Nothing fails when the two disagree, so review is the whole defence, and review is what the busiest week takes away first, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: One language across the seam, or two.

## Counter-evidence and transfer limits

The sources are specifications and one design essay, not measurements.
Nothing in the ledger compares a generated seam with a hand-maintained
one, so B stands on one recorded estate failure and on the
rotting-artefacts lesson, which is two ventures' local observation. The
tools that stop code importing around the generated client see static
imports only (EV-0147, EV-0148), so a hand-written fetch to a literal
URL is invisible to both. D rests on JSON Schema's claim about failing
loudly (EV-0025) and on an essay about types (EV-0285), neither of which
observed a venture or priced the runtime cost. And consumer-driven
contracts answer what neither B nor D asks, whether the deployed pair
was ever verified (EV-0193). No venture runs one.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
