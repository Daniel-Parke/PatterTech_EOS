---
summary: How frontend and backend come to agree on types, whether hand-maintained, generated and gated, one language end to end, or parsed at the edge
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0023, EV-0025, EV-0057, EV-0147, EV-0148, EV-0193, EV-0285]
review: 2027-07
type: guide
tags: [arch, ci, tooling]
review_by: 2027-07
---

# WG-ARCH-005: how do frontend and backend agree on types?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. Two things changed. The gate is now the part
that binds, as B4 of `packs/architecture/PACK.md`, while the choice
between options stays a default. And a fourth option arrived, parsing
at the edge, because generation proves what compiled and says nothing
about what is running.

## The question

Two codebases describe the same request and the same response. The fork
is what keeps them agreeing: discipline, generation, unification, or
parsing. The failure that decides it is the quiet one, where a renamed
field makes a mutation fail and the interface reports success. The
option you take sets when that failure surfaces: at review, at build,
or in front of a user.

## It depends on

- One language across the seam, or two.
- Whether generation can run offline and deterministically, with no
  live server needed to know the contract.
- Whether both sides ship from one commit, or drift apart in production.
- Who else calls the boundary, and whether you can rebuild them.
- Whether the client's model should be the wire shape at all.

## Options

### A. Hand-maintained client types

**What it is.** The client declares the shapes it needs and a person
keeps them in step.

**Buys.** No build step, and the client models what the interface needs
rather than what the handler returns. The only option left when the
other side publishes no schema.

**Costs.** Nothing fails when the two disagree. No artefact means
review is the whole defence, and review is what the busiest week takes
away first.

### B. Generated from the schema, committed, drift-gated

**What it is.** The schema is emitted from the API offline and
deterministically (EV-0023) and compiled into a committed types package
and a typed client that checks the response succeeded. A CI test fails
when the committed copy lags its source, and a boundary rule forbids
importing around that client: import-linter's forbidden contract
(EV-0147), or dependency-cruiser's no-reaching-into-internals rule
(EV-0148).

**Buys.** A backend change the frontend has not absorbed becomes a red
build in the commit that made it.

**Costs.** Build-time agreement only: it proves the client compiled
against a schema, not that the deployed server matches it. The
generated surface is the wire shape, so handler habits reach the
interface. Without a failing check the artefacts rot, a lesson
`registry/LESSONS.md` records from experience.

### C. One language end to end, types shared as source

**What it is.** tRPC-style inference, or a models package both sides
import. No generator and no artefact; the compiler is the contract.

**Buys.** The seam disappears. A rename is a compile error in the same
commit, and there is nothing to keep deterministic and nothing to rot.

**Costs.** Unavailable across Python and TypeScript, which is most of
this estate. It couples release, since shared source is true only while
both sides ship together, so a client on last week's bundle believes a
contract the server has stopped honouring. No outside consumer has an
artefact to read either.

### D. Schema at run time, parsed at the edge

**What it is.** One schema artefact describes the wire (EV-0025) and
each side parses what arrives against it, narrowing to a domain type at
the boundary instead of re-checking fields downstream (EV-0285).

**Buys.** The failures B cannot see: a deployed server that no longer
matches its published schema, a proxy dropping a field, a stale client.
Each becomes a located failure carrying the payload, and it needs no
type system on either side.

**Costs.** It fails after deployment rather than before, it costs
something on every request, and an unparseable response is a
user-visible outcome somebody has to design.

## Decision rule

Two languages across the seam: **B**, always, generation offline and
the artefacts committed. B4 binds the gate, not the choice of option.
Add **D** where the two sides can be deployed apart, or where the other
side is not yours to rebuild; the pairing is deliberate, since B fails
at build time and D fails at run time. One language, one repo, one
release: **C** is legitimate, with the same commit-and-gate discipline
for anything that leaves the repo. **A** is the ruling only where the
other side publishes no schema, and then the adapter is one file tested
against recorded payloads. Whichever wins, freeze the interface and
leave the internals alone (EV-0057).

## Default

**B**, which is also the seam rule of stack profile 03
(`registry/stacks/STACK-fullstack-app.md`). The estate runs Python
services under TypeScript fronts, so the seam is generated, committed
and gated, or it lies. Where the boundary is public,
`packs/api-integration/PACK.md` rules who authors the contract and how
it is versioned; this guide rules only how the types cross.

## Worked rulings

- **WiseWattage (2026, argued)**: B. OpenAPI generated from the FastAPI
  app into a committed types package and typed client, with the drift
  check in CI. The stack profile was drawn from it.
- **PatterStudio (2026-06, argued)**: B, in its ADR-0006, after failed
  mutations masqueraded as success in a plain-JS client. The
  always-check-the-response rule is written into the seam and is now
  check A-13 of `packs/architecture/CHECKS.md`.
- **AutoWatt (2026-07, inherited)**: B, taken with stack profile 03 per
  its ADR-0002, no separate argument recorded.
- **No venture runs C or D.** C never arises, because every venture with
  a backend runs Python under TypeScript. PatterStage's one HTTP adapter
  onto a third-party agent runtime is where D gets argued first.

## Counter-evidence

The sources are specifications and one design essay, not measurements.
Nothing in the ledger compares a generated seam with a hand-maintained
one, so B stands on one recorded estate failure and on the
rotting-artefacts lesson, which is local observation across two
ventures. The tools that stop code importing around the generated
client see static imports only (EV-0147, EV-0148), so a hand-written
fetch to a literal URL is invisible to both and the bypass rule is
partial. D is argued from JSON Schema's own claim about failing loudly
(EV-0025) and from an essay about types (EV-0285); neither observed a
venture, and neither priced the runtime cost. Consumer-driven contracts
answer the question neither B nor D asks, whether the pair actually
deployed together was verified (EV-0193). No venture runs one because
the same person deploys both sides, and that reason expires the day it
stops being true.
