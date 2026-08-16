---
summary: The pack contract for identity, structure, progressive disclosure, admission and activation
type: governance
tags: [eos]
---

# PACK_CONTRACT

A knowledge pack is one domain's activation surface, outcomes, limits and
decision map. Its directory is a stable machine key. Its `display_name` is the
reader-facing name, its `category` groups it in the generated index, and its
`id_namespace` owns new Doctrine, Wargame, Relation and example identifiers.
`kernel/NAMING_SPEC.md` defines those names.

Packs use three levels of disclosure. The first prose paragraph of `PACK.md`
appears in `packs/INDEX.md`. The rest of `PACK.md` loads when the pack
activates. Atomic knowledge and supporting material load only when cited.

## Required structure

Every built pack contains:

- `PACK.md`, with `kind: record`, `type: pack`, `display_name`, `category` and
  `id_namespace`. Its body owns activation, outcomes, non-goals, failure modes,
  counter-evidence and the decision map. It links to Doctrine and Wargames
  without restating their normative content. Compatibility anchors may retain
  old fragment links without becoming a second source of truth.
- `CHECKS.md`, with `kind: record` and `type: checks`. It separates what a
  machine can verify now from what still needs judgement.
- `doctrines/`, containing one atomic `DOC-<NAMESPACE>-NNN` file per standing
  proposition.
- `wargames/`, containing recurring decision procedures. Every live Wargame
  has a canonical `WG-<NAMESPACE>-NNN` identity.
- `examples/`, containing worked examples with `EX-<NAMESPACE>-NNN` names.
- `references/`, containing supporting mechanics, cards and tables too long
  for `PACK.md`.
- `research/`, containing source synthesis and drill material rather than
  operational Doctrine.

The five collection directories exist even when one is temporarily empty, so
the shape is predictable. A pack adds `relations/` only when it owns typed
`DREL-*` Relations. A Relation sits at the pack root because it may connect
more than one knowledge class.

No live pack uses the retired decision-procedure collection, worked-example
collection or abbreviated reference collection. Historical paths remain
available from the Git commit that contained them, not through redirect files
in the current tree.

## Definition of done

A pack is implemented only when it contains all of:

1. Activation paths and applicability predicates.
2. Desired outcomes and non-goals.
3. Atomic Doctrine with binding, default, advisory or preference authority,
   linked from the pack without duplicated normative prose.
4. At least three materially different patterns or philosophies where genuine
   alternatives exist.
5. A Wargame stating when each material pattern fits.
6. Trade-offs, failure modes and anti-patterns.
7. At least one worked example.
8. Evaluation criteria or executable checks where appropriate.
9. At least three maintained primary or official sources, with published
   repositories where available, each represented by an evidence-ledger row.
10. Counter-evidence or documented disagreement between sources.
11. Version or commit, licence, access date and review trigger for every
    source.

## The pruning test

For every line ask whether removing it would cause an agent to make a mistake.
If not, cut it. Versioned facts belong in `registry/` and are cited rather than
copied into standing Doctrine.

One recurring decision belongs in one Wargame. A second independent question
gets a new Wargame and a cross-link, not a sub-number. Tightly coupled pressure
dimensions may share a Wargame only when each remains separately addressable
and ruleable in its body and pressure mapping.

Files admitted under one evidence packet may declare one `review_cohort` when
a joint semantic and coverage review genuinely revalidates all of them. Cohort
members share one non-empty slug and one dated review. Source-specific
freshness remains in the evidence and Relation records.

## Activation

Every pack declares machine-readable activation in its own front-matter:

- `activation_paths`, with globs where `**` crosses directory separators and
  `*` does not;
- `applies_when`, using the controlled predicates in
  `kernel/PREDICATES.md`.

At least one trigger must be a path pattern or task predicate rather than a
keyword. `python -m tools.eos context` evaluates paths, and
`python -m tools.eos activate` evaluates declared facts. Given the same facts,
activation and dependency order must be deterministic.

Applicability is the real gate. A path match with no satisfied predicate does
not load the pack body. Activation supplies knowledge only. It never lowers a
tier floor in `kernel/POLICY_SPEC.md` or grants an action forbidden by
`kernel/GUARD_SPEC.md`.

## Domains below the admission bar

A domain that cannot meet this contract stays in `registry/coverage.json` with
`status: registry-only`, a reason and a reopening trigger. It has no stub pack
directory and is never described as implemented. `packs/INDEX.md` lists built
packs; `registry/CAPABILITIES.md` shows built and registry-only domains
together. An omission is a row, not a silence.
