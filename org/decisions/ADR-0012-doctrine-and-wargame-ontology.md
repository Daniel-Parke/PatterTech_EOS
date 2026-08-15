---
summary: First-class graded Doctrine and one semantic Wargame model over stable procedure identities
type: decision
tags: [eos, wargame]
status: accepted
decided_by: Daniel Parke
date: 2026-08-15
---

# ADR-0012: Doctrine and Wargame ontology

The operator approved this rebuild on 2026-08-15. The approval named the
ontology, the migration order, the acceptance conditions and the boundary
against releases and venture rewrites. This record settles the knowledge
shape. ADR-0013 settles compatibility and venture records. ADR-0014 settles
what new content is allowed in.

## Context

The live tree has 25 packs and 114 decision procedures, but a reader sees 100
`GD-*` records and only 14 `WG-*` records. Doctrine is harder to see. At least
501 normative source blocks sit inside mixed pack prose and no first-class
Doctrine catalogue exists. The labels describe history rather than the
semantics the operator expects.

Renaming the 100 `GD-*` records would make the surface look tidier and break
identity. Architecture already has both `GD-ARCH-001` and `WG-ARCH-001`.
Aliases cannot preserve raw paths, old GitHub links or lookups at a pinned
commit. The two-pack spike at
`org/reports/DOCTRINE_WARGAME_SPIKE_2026-08-15.md` kept both identities,
extracted 39 normative blocks without a second source and reduced the loaded
context by 22.90 per cent.

## Decision

**One. Doctrine is the public umbrella for standing rules.** Its authority is
one of four grades.

- Binding holds whenever its applicability is true. A Wargame cannot waive
  it. Contrary evidence opens a doctrine review or an ADR.
- Default is inherited unless pressure and an argued ruling justify departure.
- Advisory informs judgement without requiring a departure record.
- Preference is optional taste or convenience. A brand-scoped preference
  activates only through explicit adoption.

**Two. One atomic file is the canonical source for one proposition.** It lives
at `packs/<pack>/doctrines/DOC-<PACKCODE>-NNN-<slug>.md`. Its metadata records
the statement, authority, basis, evidence grade, scope, applicability,
challenge triggers, sources, review, lifecycle and verification references.
The ID does not encode authority. A changed grade or evidence set keeps the ID
while the proposition remains the same. A material change to prescription or
scope creates a successor ID and bidirectional supersession.

**Three. A pack is the activation and navigation surface.** `PACK.md` keeps
activation, outcomes, non-goals, the compatibility map and the decision map.
It links DOC IDs and does not retain a second normative copy. Explicit HTML
anchors preserve legacy `B`, `D`, `BR` and `H` fragments.

**Four. Wargame is one semantic type.** Every current `GD-*` and `WG-*`
procedure becomes `kind: wargame` and `type: wargame`. Existing IDs and paths
are immutable. New procedures use `WG-*`; no new `GD-*` identity is issued.
The historical `guides/` directory remains a compatibility storage name.

Every Wargame states its modes from `selection`, `conflict`, `exception` and
`gap`; the doctrines or gap under pressure; applicability and engagement
predicates; options; a premortem for every credible option; a decision rule;
a safe default or why none is safe; the cheapest discriminating test; a named
fallback, exit and revisit trigger; and counter-evidence and transfer limits.
Worked executions are Rulings, not mutable history copied into the procedure.

**Five. Relations are typed records owned beside the deciding doctrine.** A
`DREL-*` relation may be `depends_on`, `supports`, `tensions_with`,
`conflicts_with`, `exception_to`, `supersedes` or `covers_gap`. It records its
conditions, state, evidence, fallback and covering Wargame. The estate-wide
pressure matrix is generated, never hand-edited.

**Six. Authority is reconciled during migration, not inferred from headings.**
Every one of the 501 frozen source blocks receives `create`, `merge_into`,
`retain_explanatory` or `reject`, with a reason and destination. Decision-only
binding propositions become defaults unless qualifying evidence or an
accepted ADR earns binding. The security floors in security-privacy and the
production-safety floors in devops-reliability retain the exemption already
settled by ADR-0008.

## Consequences

This adds many small files and makes the proposition, rather than the pack
paragraph, the unit of review. Generated indexes and a shared resolver must
keep that estate navigable. Exact duplicate statements become errors;
semantic merges remain reviewed decisions.

The migration may split a source block where its clauses can be departed from
independently. It may also merge duplicate propositions across packs. It may
not silently lose a source block, change an existing procedure identity or
turn a preference into estate law.

Rollback is phase-based. Until every ledger row and compatibility alias is
green, the original pack text remains recoverable at the frozen commit. A
failed pack transaction reverts its atoms and router together.
