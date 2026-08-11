---
summary: How the pack activation walk is built, the always-walk set, the canonical order over every pack and the two ruling budgets
type: kernel
tags: [eos]
---

# WALK_ORDER

How phase C of inception/INCEPTION.md builds the list of guides a
venture actually rules, and the order it rules them in. It stays
bounded by design: only activated packs are walked, and everything else
inherits its default silently and costs nothing.

## Build the walk

1. Match the surfaces, domains and risk answers the interview gave
   against each pack's own `activation_paths`, by hand. That match is
   the walk's input, not `packs/INDEX.md`: the index is for a human
   reading, and a walk built by eye off it reads every row in it. The
   `python -m tools.eos context` command narrows the same front-matter
   from a diff, but it diffs this repository and has no venture-tree
   mode, so at Session 0, before the venture has a history, there is
   nothing for it to read.
2. Confirm each candidate pack's predicates, which are the real gate: a
   pack that trips a path trigger and satisfies no predicate loads
   nothing beyond its first paragraph and is not walked. Put the answer
   in that pack's ruling note, so the next walk reads it rather than
   asking again.
3. For every kept pack, walk the guides under its guides directory.
   Guides with WG- ids walk like any other.

Domains with no built pack are not gaps in the walk. Each carries an
honest row in registry/CAPABILITIES.md, and a fork landing in one takes
the draft-guide route below.

## The always-walk set

Three things are walked whatever the triggers say.

1. WG-EOS-001, the scale ruling, before any pack. It gates the matrix
   column and the ceremony of everything after it.
2. WG-EOS-002, the repo shape.
3. The security-privacy pack. Its predicate runs_agents holds for every
   governed venture by construction, because the seed exists so agents
   can work in the repo, and its binding requirements are protected-set
   subjects.

## Canonical order

Every pack has a place, so no walk has to invent one. Structure comes
before surface, proof comes before operation, and the agentic packs come
last because their choices consume the rulings above them. Ascending id
within each step.

1. WG-EOS-001, scale.
2. WG-EOS-002, repo shape.
3. security-privacy, which is always walked, then legal-licensing when
   it activates. The floors and the law. Nothing below may lower either.
4. product-discovery, business-model-pricing. What is being built and
   what it sells. These come before structure because structure argued
   against a moving subject gets argued twice.
5. business-logic-modelling, architecture, api-integration,
   data-analytics. The domain rules, then the boundaries inside the
   code, then the boundaries it publishes, then the event and analytics
   contracts.
6. ai-ml-llm, coding, delivery-testing. What the code calls, how it is
   written, how it is proved.
7. devops-reliability. Operating what the steps above produce.
8. ui-ux, native-client, writing-content, docs-dx, pattertech-house.
   Surfaces, in the order they depend on each other: ui-ux carries the
   portable interface law, native-client carries the non-web
   accessibility profile ui-ux defers to, and pattertech-house rules
   last because it is taste sitting under all of it and activates only
   by adoption.
9. marketing-growth, support-operations. Reaching people who have not
   arrived, then serving the ones who have.
10. agentic-development, then agentic-swarm. Agents built into the
    product, then how the venture builds with agent graphs. The swarm
    ruling reads the dependency graph and the oracle out of steps 5 and
    6, so it cannot be taken before them.

Every row of packs/INDEX.md is placed above. A pack added later joins
the step it depends on, and one added without being placed here leaves
the next walk to guess.

A guide whose decision rule names another guide's ruling as an input
jumps behind that prerequisite. Where two packs genuinely conflict, the
decision belongs to the pack that owns it under GOVERNANCE.md
precedence, and the stricter rule applies until a joint guide exists.
No activation lowers a tier floor or converts a manual-only action
class into an autonomous one.

## Record the rulings

Every walked guide lands as one rulings row in the lock-book header,
id · ruling · argued|inherited · note. Argued means the venture's facts
were engaged afresh against the guide's fork, and any guide a trigger
names must be argued. Inherited means the default was taken without new
argument, legitimate when the triggers are silent, and never promotion
evidence.

A fork no guide covers: file a draft guide in docs/EOS_FEEDBACK.md with
the question, the options seen, the decision rule used and the
venture's ruling as its first worked entry. Record the ruling as
GD-DRAFT-NNN, numbered per venture; the harvest assigns the real pack
and id later and rewrites the row.

## Budget

Two counts, not one, because they mean different things and only one of
them can indict a ruling. Count them separately as you walk, and write
the pair into docs/COMPILE_REPORT.md beside the check results, as
N interview-triggered and M doctrine-triggered. The lock-book's rulings
rows stay the record of what was ruled; the pair is what says whether
the walk stayed in shape.

**Interview-triggered rulings** are the ones the venture's own answers
demand. A trigger names a fork, so the fork gets argued. Budget twenty.
Past twenty, either the trigger set is too broad or the venture is
bigger than its scale ruling. Stop, re-run WG-EOS-001 with the operator,
and start again from the new ruling.

**Doctrine-triggered rulings** are the ones a pack brings with it. The
pack activated, so its guides get walked, whether or not the operator
ever raised the subject. This count is a function of how many packs
activated and how many guides each holds, so it cannot indict the scale
ruling and must never re-run WG-EOS-001 on its own. A venture whose
master prompt fixes deep product doctrine legitimately walks long. Past
twenty of these, split the walk over two sittings and finish before
phase D.

An S venture with a single surface typically activates two or three
packs and rules under a dozen guides in one sitting. Guth's walk ran to
thirty-two rulings and was recorded as an overrun, because the twenty
was written for the interview-triggered kind and then applied to both
kinds added together. Both numbers here are starting values with that
one walk behind them, not measurements; a walk that beats either of them
for a reason it can state is worth more than a walk that came in under.
