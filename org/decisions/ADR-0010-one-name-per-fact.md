---
summary: A controlled vocabulary for pack activation predicates, grouped by subject, with the first duplicate merged
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-15
---

# ADR-0010: one name per fact

Daniel authorised this on 2026-08-15 as part of the audit and expansion
mission, having asked that the estate expand so an agent has more to
draw from, and that the AI bring only the packs a venture needs. This
record is the second of those, because the first breaks it.

## Context

Pack activation runs on predicates. Each pack declares `applies_when` in
its own front-matter, which `packs/PACK_SHAPE.md` calls the real gate,
and `python -m tools.eos activate` now computes the Session 0 walk from
them.

The estate declared 88 predicates and 87 were owned by exactly one pack.
That reads like tidy separation and is not. There was no list, so a pack
author had nowhere to look before naming a fact, and the names were
checked against nothing.

One duplicate had already landed. `security-privacy` declared
`handles_personal_data` and defined it as "any processing of
identifiable people". `legal-licensing` declared
`processes_personal_data` and defined it as "the system collects, stores
or transmits data about identifiable people". Those are the same fact,
and both are the answer to interview question 9, "does it touch personal
or regulated data, anyone's". Each pack was internally correct.

The consequence is not cosmetic. A venture recording one spelling loads
one pack and silently misses the other. Missing a pack is the expensive
direction: the seed ships without the ruling and nothing in it says so.
`eos activate --predicate handles_personal_data` returned
`security-privacy` alone, which is how this was found.

Adding four more packs multiplies the surface. Retrofitting a vocabulary
across 25 packs is more work than establishing one across 21, and the
next duplicate is likelier than the last, because the obvious subjects
are taken.

## Decision

**One.** `kernel/PREDICATES.md` is the controlled vocabulary. A pack may
only put a name in `applies_when` that appears there.

**Two.** It is grouped by subject, not by pack. That is the whole
mechanism. A list sorted alphabetically puts `handles_personal_data` and
`processes_personal_data` twenty rows apart; a list grouped by subject
puts them adjacent, where the person adding a third sees them. Nothing
else in this decision prevents a duplicate. The grouping does.

**Three.** Sharing a predicate across packs is normal and expected.
`handles_personal_data` now activates both `security-privacy` and
`legal-licensing`, and `runs_experiment` already activated both
`data-analytics` and `product-discovery`. Two packs naming one fact is
two packs agreeing about the world, not a coupling between them.

**Four.** A predicate is a fact an operator can answer yes or no about
the venture, not a judgement about the work. `has_database` qualifies.
`needs_careful_design` does not.

**Five.** `processes_personal_data` is retired in favour of
`handles_personal_data`, and retired names are never reused. The plainer
spelling wins on the house voice rule, and it is the broader act:
holding data is covered by handling it and is not obviously covered by
processing it. `legal-licensing` keeps its own duties on the shared
fact, which is what the vocabulary row records.

**Six.** Check S021 holds pack front-matter to the file, at error
severity. It reports a retired name separately from an unknown one,
because the fixes differ: an unknown name is a new fact somebody has to
add, and a retired name is a fact that already has a spelling.

## Counter-evidence and what argues against this

**A central list is the coupling this repository usually refuses.**
`packs/PACK_SHAPE.md` says the pack owns its triggers so there is no
second list to drift. This adds one. The answer is that it is a
vocabulary and not a second copy: the pack still declares which
predicates apply to it, and the file declares only that a name exists
and what it means. S021 makes drift a build failure rather than
something to notice later, which is the condition ADR-0008 sets for a
rule that binds.

**Error severity on a naming rule is heavy.** A pack author who invents
a name now fails the build. That is deliberate. The failure it prevents
is a venture missing a pack it needed, which is silent, and reaches the
seed, and is discovered by whatever goes wrong later.

**Grouping is a judgement and judgements drift.** A predicate can
plausibly sit in two groups, and somebody will file one badly. That
costs a duplicate eventually. It still beats no grouping, and the cost
of a misfiled row is one duplicate rather than the current position,
which is no mechanism at all.

**Interview questions are not yet mapped.** The vocabulary says what
makes each predicate true, but does not yet name which interview
question settles it. Until that lands, an operator still has to assert
the facts rather than have them derived from Session 0 answers. That is
the next piece of work and it is recorded in
`org/reports/NEXT_TRANCHE.md` rather than claimed here.

## Migration

Four authored files changed: `packs/legal-licensing/PACK.md`, its
exemplar `EX-LEGAL-001`, and `registry/coverage.json`, whose derived
view regenerates. No venture is affected: no seed fixture and no
governed venture records an adopted pack, so nothing downstream carries
the retired spelling. Any that did would fail S021 and be told which
name to use.
