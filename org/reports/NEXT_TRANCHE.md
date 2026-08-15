---
summary: What the audit and expansion mission completed, what it deliberately did not, and the dependency-ordered work that follows
type: org
tags: [eos]
---

# The next tranche

Written 2026-08-15 at the end of the first tranche of the audit,
research and expansion mission, on `eos/audit-research-expansion`. The
mission brief asked for an audit, full external research waves and a
large expansion of the knowledge base. This records what landed, so the
next session starts from a line rather than a wish.

## What landed

Fifteen commits. `python -m tools.eos check` reports no errors and the
one known warning; the suite went from 513 tests to 576.

- **Baseline** recorded in `org/reports/BASELINE_2026-08-15.md`, so
  every later claim about growth or proportionality has a before half.
- **Correctness repairs**: drill verdicts recorded where 22 nulls stood;
  the dependency lock made true on more than one machine, which it was
  not; check S020 for a derived view claiming git was unavailable; the
  seed series run over the one fixture nothing checked; `task new` now
  says when it ruled a tier from an empty fact set.
- **Audit deliverables**: `org/reports/CONTROL_ENFORCEMENT.md` and
  `org/reports/DEFECT_REGISTER_2026-08.md`.
- **Activation**: `eos activate` computes the Session 0 pack walk from
  declared venture facts or straight off a brief's ```facts block, names
  the packs left out and why, and exits 1 on a predicate no pack owns.
  Measured across eight venture archetypes.
- **Coverage**: the seven domains no pack owns are registry-only rows in
  `registry/coverage.json` with their reasons, so the matrix reads 21
  built and 8 registry-only rather than as though the packs were the
  whole map.
- **ADR-0009**, accepted: the line is renumbered to 0.4.0 and 1.0 now
  means an eight-item gate somebody can run or read. No tag is cut, so
  nothing is released.
- **ADR-0010**, accepted: the controlled predicate vocabulary, check
  S021, and the first duplicate merged.

## What did not land, and why

The research waves and the pack expansion did not start. That is a
deliberate stop, not an overrun. The design pass measured one pack at 23
to 41 hours to meet the existing eleven-point definition of done plus a
frozen drill, so four packs is 92 to 164 hours. Starting that and
stopping halfway would have left partially built capabilities, which
the mission brief forbids and which `packs/PACK_SHAPE.md` calls
shallow completeness.

Three findings from this tranche also change how that work should be
done, and doing the expansion first would have meant redoing it.

## The dependency order that follows

**One, the predicate vocabulary. Done, 2026-08-15.** ADR-0010 landed it:
`kernel/PREDICATES.md` is the controlled vocabulary, grouped by subject
so two names for one fact sit adjacent, and check S021 holds pack
front-matter to it at error severity. The collision that prompted it is
merged, so `handles_personal_data` now activates both `security-privacy`
and `legal-licensing`.

Each row also records what settles it. Of 87 predicates, 59 are venture
facts answerable at Session 0, 27 are task facts that are not knowable
until the work exists, and one is always true. That constrains anything
built on top: a Session 0 flow cannot settle roughly a third of the
vocabulary, whatever it asks.

**Two, the activation corpus. Mostly done, 2026-08-15.**
`tests/fixtures/activation/profiles.json` holds eight venture
archetypes, from a disposable script to a SaaS with subscriptions, and
`tests/test_activation_corpus.py` measures precision and recall per
pack with negative cases, which is 1.0 gate item 5. Both are 1.000
across 49 expected activations. The venture brief template now carries a
```facts block and `eos activate --brief` reads it, so the walk can be
computed from what the operator answered.

Two things are still open here. The expected lists were authored in the
same commit as the code that satisfies them, which is the Wave B
guarantee rather than the Wave A one, so a later pass should freeze
expectations for the four admitted capabilities before their predicates
are written. And eight archetypes is a start, not a corpus: the mission
brief names twelve.

The corpus already earned its place by surfacing something the design
passes missed. Three packs, `agentic-swarm`, `coding` and
`product-discovery`, declare nothing but task facts, so no Session 0
interview can activate them however it is answered. They activate when
work arrives, through `eos context`. That is correct, and it means a
compiled seed's pack walk can never include them.

**Three, seed proportionality.** `packs_adopted` is empty in both seed
fixtures and in all three ventures, so the pack-adoption path has never
run end to end and no fixture exercises it. Before the library grows,
capture what a seed costs: bytes, files, lock-book ruling rows and the
lines a task actually reads. Today that is 9 files and 30,890 bytes at
S, and 20 files and 65,440 bytes at ORG. Without that baseline there is
no way to show a bigger library did not make bigger seeds.

**Four, the research programme.** The pipeline design exists and its
constraints are in the plan. Two repairs belong to it rather than to a
content wave: `licence` carries 249 distinct values across 504 records,
which is realised taxonomy drift with a single writer; and
`GOVERNANCE.md` says the checker enforces bidirectional supersession
while S002 reads markdown front-matter only and the evidence ledger has
no supersession fields at all. Also here: the 23 empirical records with
no counter-evidence, the 22 stale rows and the one url-dead, and the 268
records whose `on-change-of:` review nothing watches.

**Five, the expansion.** Then, and only then, the capabilities. The
evidence-led ranking from the design pass, each through the admission
gate, each with a drill frozen before its pack is authored:
`identity-access`, `supply-chain-integrity`, `data-engineering` and
`research-knowledge`, with guides into `architecture`,
`devops-reliability`, `native-client`, `ui-ux` and
`agentic-development`. The registry-only rows for all seven are already
in `registry/coverage.json`, so building one is a promotion rather than
a new entry, and abandoning one leaves an honest row behind rather than
a silence.

Two holes to close in the same pass: `delivery-testing` has no `GD-`
guides at all, and `agentic-swarm`, the pack the estate itself runs on,
has no frozen drill.

## The honest headline on scale

Daniel asked to massively expand the packs so an agent has more to draw
from. The first wave is 21 packs to 25, with substantially more depth
inside the existing ones. Going straight to 45 means inventing decision
surfaces that do not exist, which fails the admission gate the estate
already has. The architecture in `eos activate` and the level-0 index
work is what makes 45 reachable later; the content should arrive as
ventures produce the non-activation cases that prove a pack is real.
