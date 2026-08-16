---
summary: One current vocabulary for Doctrine, Wargames, relations, Rulings and packs, with explicit historical compatibility
type: decision
tags: [eos, wargame]
status: accepted
supersedes: [ADR-0012, ADR-0013]
decided_by: Daniel Parke
date: 2026-08-16
---

# ADR-0015: one language for Doctrine, Wargames and packs

The operator asked for the whole repository to use terminology that is
correct, descriptive and succinct. In particular, a Wargame must not present
itself as a `GD-*` Guide stored in `guides/`. This record replaces ADR-0012
and ADR-0013 in full. It restates their surviving ontology and compatibility
decisions, then settles the clearer current naming contract. ADR-0014 remains
the authority for content admission.

## Context

The Doctrine and Wargaming rebuild made all 127 decision procedures semantic
Wargames, but retained 100 `GD-*` identities and 125 files under `guides/`.
That preserved old locations at the cost of making the public tree contradict
its own vocabulary. A reader could reasonably conclude that the repository
held only 27 Wargames.

The inconsistency is wider than two names. Packs use mixed human titles and
metadata types, `CHECKS.md` uses five metadata shapes, worked examples live
under `exemplars/`, references under `refs/`, and relations beneath Doctrine
although a relation joins more than one entity. Some generated views retain
compatibility names as if they were current products. Many Doctrine filenames
also stop in the middle of a word because their slug was cut by character
count.

The frozen T-0028 inventory records 25 stable pack slugs, 516 Doctrines, 127
Wargames, 19 relations, all identifier collisions and the exact target paths.
An independent oracle was committed before implementation.

## Options considered

1. **Change prose only.** This preserves every path but leaves the strongest
   public signals, identifiers and collection names, saying the wrong thing.
2. **Use one clean current vocabulary, with identifier aliases and pinned Git
   history for compatibility.** This makes the live tree truthful while
   retaining deterministic resolution of old identities and old commits.
3. **Keep redirect files at every old path.** This preserves more current-branch
   links, but leaves 125 non-canonical files in the live knowledge surface and
   creates two apparent locations for each procedure.
4. **Rename pack directories and prefix them by category.** This makes grouping
   visible in paths, but turns presentation into identity and causes broad path
   churn without improving the meaning of a pack once it is open.

Option 2 is accepted. Pack directories remain stable and gain separate display
and category metadata. Redirect files and category prefixes are rejected.

## Decision

### One current knowledge vocabulary

`Doctrine`, `Wargame`, `Relation` and `Ruling` are EOS entity classes and take
a capital letter when that class is meant. `Wargaming` is the act of applying
a Wargame. Lowercase `guide` remains an ordinary document description, such as
an operator guide or style guide, and is not a decision entity.

Doctrine remains the umbrella for standing propositions. Its authority is
`binding`, `default`, `advisory` or `preference`. Binding Doctrine cannot be
waived by an ordinary Ruling. A material change to a proposition or scope
creates a successor identity; evidence or authority changes retain the
identity while the proposition remains the same.

One Wargame remains one recurring decision procedure. It carries selection,
conflict, exception or gap modes; applicability and engagement predicates;
materially different options and their premortems; a decision rule; safe
default or an explicit absence of one; the cheapest discriminating test;
fallback, exit and revisit conditions; and counter-evidence and transfer
limits. A Ruling is one venture applying one Wargame, not history embedded in
the Wargame.

### Canonical identifiers and aliases

Every live current Wargame uses `WG-<NAMESPACE>-NNN`. No new `GD-*` identity is
issued. The 103 old identities in `org/migration/NAMING_BASELINE.json` map to
one collision-free canonical target each. They remain aliases, not retired
identities, because a live venture may still cite one at an older EOS pin.

The shared resolver canonicalises an alias before duplicate checks, selection
and Ruling comparison, always-walk enforcement, include or omit handling and
generated output. A current lookup of an old identity returns the canonical
Wargame and records the requested alias. A lookup at a historical commit uses
the identity and path defined by that commit and never falls forward to the
worktree.

`RUL-*` remains document-scoped. It is unique within one venture
`docs/RULINGS.json`, not across the estate. `DOC-*`, `DREL-*`, `WG-*`,
`ADR-*`, `EV-*`, `LES-*`, `LENS-*`, `T-*`, `PB-E*`, `EX-*` and `STACK-*`
retain their existing meanings. New Wargame and Doctrine namespaces use the
owning pack's `id_namespace`. A new Relation uses the namespace of its owning
Doctrine. Historical Relation namespaces are not renamed merely because the
record sits in another pack.

### Canonical collections and public files

A built pack uses these collection names:

- `doctrines/` for atomic standing propositions;
- `wargames/` for decision procedures;
- `examples/` for worked examples;
- `references/` for supporting mechanics and tables;
- `research/` for source synthesis and drill material;
- optional `relations/` for typed Doctrine relations.

The pack contract is **packs/PACK_CONTRACT.md**. The generated alias view is
**registry/IDENTIFIER_ALIASES.md**. `packs/WARGAME_INDEX.md` is the sole current
procedure catalogue. There is no current `GUIDE_INDEX.md`.

Old Git commits preserve old paths and remain readable through an explicit
pin. Current identifier aliases do not pretend to preserve branch-relative
GitHub or raw-content URLs. The live tree carries no redirect stubs at retired
collection paths. This cost is stated rather than hidden.

### Pack identity and presentation

The 25 lowercase kebab-case pack directories remain stable machine keys. A
pack declares `display_name`, `category` and `id_namespace` in `PACK.md`.
Display names are concise domain names, not filenames with `Pack`, `EOS` or a
category prefix added. The generated index groups packs into six presentation
categories:

- Data and AI;
- Engineering;
- Experience and Content;
- Practice and Governance;
- Product and Commercial;
- Reliability and Trust.

Categories help navigation and do not alter activation, dependency order or
identity. The exact one-for-one mapping is frozen in the T-0028 inventory.

### Metadata and filenames

Every `PACK.md` is `kind: record`, `type: pack`. Every invariant `CHECKS.md`
is `kind: record`, `type: checks`. A worked example is `kind: example`,
`type: example`. Doctrine and Wargame retain matching `kind` and `type`
values. Historical lesson disposition `decision-guide` becomes `wargame` in
the current registry and schema.

A Doctrine filename begins with its immutable DOC identity and a descriptive
lowercase kebab-case slug. The full basename is at most 72 characters and the
slug ends at a word boundary. A path change does not change the Doctrine
identity or proposition.

### Relations, matching and Rulings

A `DREL-*` Relation remains one of `depends_on`, `supports`, `tensions_with`,
`conflicts_with`, `exception_to`, `supersedes` or `covers_gap`. It records its
conditions, state, evidence, fallback and covering Wargame. The estate-wide
pressure matrix remains generated.

Matching remains tri-state. True pressure requires a Wargame. False pressure
records omission. Unknown high-consequence pressure asks or includes; unknown
routine pressure produces a candidate. Scale, repository shape and security
floors remain always-walk decisions. Operators may include or omit candidates
with a reason, but cannot omit an always-walk Wargame. Matching explains its
selection and never chooses the outcome.

New ventures continue to own structured `docs/RULINGS.json`. Default
departures require a reason; binding-scope changes require an ADR or operator
reference. Legacy delimiter rows are readable only at the schema that defined
them or through explicit migration. EOS receives only privacy-reviewed,
sanitised harvest summaries and never centralises raw venture context.

### Migration authority and historical truth

The T-0028 naming ledger is separate from the 2026-08-15 Doctrine and Wargame
content ledgers. Historical reports, frozen migrations, archive material and
accepted decision prose remain truthful snapshots. ADR-0012 and ADR-0013 gain
only their sanctioned `superseded_by` stamp.

The T-0026 ontology oracle is preserved byte-for-byte as a historical proof
of the contract it tested, outside live test discovery. T-0028 owns the new
current-tree oracle. No venture repository is rewritten by this migration.

## Consequences

The current tree becomes direct: one entity name, one current prefix and one
current collection. The change moves 125 pack Wargames, changes 103 canonical
identities, and updates every operational reference through a reviewed map.
Pack grouping improves without turning presentation labels into paths.

The cost is a deliberate break in unpinned current-branch links to retired
paths. Old commits and old identities remain resolvable, but an external link
that assumes the latest branch and an old path must be updated. Alias handling
also becomes part of every comparison boundary rather than lookup alone.

The clean vocabulary must be generated and checked. Hand-maintained totals,
secondary procedure indexes and duplicated normative prose remain forbidden.

## Verification and rollback

The migration is accepted only when the independent T-0028 oracle passes in
full, every canonical and legacy identity resolves at the appropriate pin,
the migration reaches a fixpoint, generated views reach a fixpoint, the
repository check has no findings, the full test suite passes, and a clean
clone of the pushed branch repeats those gates. Semantic normalisation must
show that Wargame and Relation content changed only by the approved naming
substitutions.

Rollback reverts the naming migration as one unit. The frozen inventory,
alias map and old Git commits provide the recovery source. Rollback does not
rewrite ventures, releases, tags, archive snapshots or the sealed benchmark.

## Applicability limits

This decision governs the current PatterTech EOS tree and future EOS naming.
It does not rename venture-owned artefacts, promise redirects for external
current-branch URLs, alter Doctrine authority, admit new knowledge, change a
Wargame outcome or release the repository. Any of those actions needs its own
authority and evidence.
