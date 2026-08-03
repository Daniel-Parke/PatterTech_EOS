---
summary: How the pack activation walk is built and ordered, the always-walk set and the budget rule
type: kernel
tags: [eos]
---

# WALK_ORDER

How phase C of inception/INCEPTION.md builds the list of guides a
venture actually rules, and the order it rules them in. Packs replace
v1's doctrine modules, so the walk starts from the pack index. It stays
bounded by design: only activated packs are walked, and everything else
inherits its default silently and costs nothing.

## Build the walk

1. Start from packs/INDEX.md, the derived index of built packs. Each
   row carries what the pack covers, what activates it, and how long
   its body is.
2. Collect the venture's trigger set: the surfaces, domains and risk
   answers the interview surfaced, plus the add-ons the scale ruling
   attached.
3. Keep a pack when a path trigger or task type in its activation cell
   matches. Then test its applicability predicates, which are the real
   gate: a pack that trips a path trigger and satisfies no predicate
   loads nothing beyond its first paragraph and is not walked.
4. For every kept pack, walk the guides under its guides directory.
   Wargames inherited from v1 keep their WG- ids and walk like any
   other guide.

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

Scale, repo shape, security-privacy, architecture, API and integration,
coding, delivery and testing, devops and reliability, UI and UX,
agentic development. Ascending id within each step. Structure comes
before surface, proof comes before operation, and the agentic pack
comes last because its topology choice consumes the rulings above it.

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

One sitting. An S venture with a single surface typically activates two
or three packs and rules under a dozen guides. Past twenty rulings the
walk has stopped being a walk: either the trigger set is too broad or
the venture is bigger than its scale ruling. Stop, re-run WG-EOS-001
with the operator, and start again from the new ruling.
