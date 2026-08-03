---
summary: The pack applied end to end to a small hosted feature whose dependency tree hides a network copyleft term, an unlicensed vendored directory and an unmade choice
kind: exemplar
scope: estate
type: example
tags: [security, pii, delivery]
---

# EX-LEGAL-001: The waitlist that pulled in more than it asked for

A worked run of `packs/legal-licensing/PACK.md` against one concrete
situation, from the first read of the task to the merge. Every rule that
fires is named where it fires. The venture sells a hosted service and
distributes nothing.

## The situation

The task is small: add an email waitlist to the marketing site. It needs
a form, a store, and a confirmation. The agent picks a well-known
library for the CSV export the founder asked for, and the repository
already contains a vendored directory copied from a public repository
some months ago. There is no privacy notice anywhere on the site.

Nothing about licences or data protection appears in the task.

## Step 1: activation

Three predicates are true, and none of them needed a keyword.
`adds_dependency`, because the task adds a library.
`processes_personal_data`, because an email address is data about an
identifiable person. `hosts_service`, because the venture's shape says
so and the pack reads that from the deployment shape rather than from
the task text.

The path trigger fires independently: the change touches a dependency
manifest and a lockfile. A task that mentioned neither licences nor
data protection has activated the pack twice over.

## Step 2: the inventory before the verdict

D2 says the scanner produces the inventory and a person produces the
verdict, so the first action is a scan over the whole tree rather than
a look at the one library being added. It returns four things worth
reading, and the pack has a rule for each.

**A transitive dependency declaring network copyleft.** Not the library
the task named, three levels below it. A distribution-shaped policy
returns nothing here, because this venture distributes nothing. Under
`packs/legal-licensing/guides/GD-LEGAL-001-copyleft-trigger.md` the
answer is option B: the obligation attaches to a modified version
reached by users over a network, and the fact that nothing is shipped
is irrelevant. B4 fires and the decision has to be written before
merge, not at release.

**A vendored directory with no licence file and no headers.** Its own
readme says it was copied from a public repository. Under B2 and the
bucket table in `packs/legal-licensing/refs/LICENCE_CLASSES.md` this is
the exclusive copyright case: absence of a licence is a refusal, and
being forkable on a hosting platform grants no right to use. Blocking
finding, bucket three.

**A dependency declaring a choice of two licences.** The inventory
holds the raw expression. Under B3 that is an unmade decision, and the
verdict column takes one identifier or the merge does not happen.

**Everything else.** Permissive, notice only, bucket one, automatic
pass with attribution collected into the notice file. Most of the tree
is boring, which is the point of a standing verdict.

## Step 3: the decision record

One artefact, `LICENCE_DECISION.md` at the venture root, written before
merge, one dated entry per finding.

The network copyleft entry names the component, its identifier, that
the trigger is remote interaction rather than distribution, and the
disposition. Here the disposition is to remove it: the export feature
can use the standard library, and substitution is cheaper than the
decision. That is option D in GD-LEGAL-001, recorded as a choice rather
than taken silently.

Had the answer been to keep it and modify it, B7 would have fired
instead. The modification boundary question is escalation trigger one
in `packs/legal-licensing/refs/ESCALATION.md`, and the correct output
would have been a one-page handover and a stopped merge, not a
paragraph of confident reasoning about program boundaries.

The vendored directory entry names the path, states that no licence was
found, and records the disposition: ask the original author, replace
it, or delete it. It does not record a guess about what the licence
probably is.

The dual-licensed entry records which of the two we take and why, and
the inventory then carries that single identifier.

## Step 4: the personal data half

An email address is personal data, so B5 fires and both halves of it
apply.

The notice goes up before the form does, carrying all ten items from
`packs/legal-licensing/refs/UK_DATA_ROUTING.md` and both complaint
routes, to the controller and to the Commissioner. The retention entry
is a real period, because the criteria version needs the criteria
written down and nobody had any.

The registration self-assessment runs separately, and its outcome goes
in the record. It is a different duty from the notice and a good notice
does not discharge it. Nobody quotes a fee figure from the pack.

Proportionality applies, from the security-privacy reference rather
than from here: one email address collected with consent for one
purpose is not high-risk processing, so no impact assessment is
written, and the reason for not writing one is recorded in a line.

## Step 5: provenance and the merge

Every commit in the change carries a sign-off line, including the ones
the agent wrote, under B6. That is a provenance record and not a claim
about authorship, because authorship of machine output is unsettled.

The merge gate now has five things to check and can check all of them
without a person: the inventory has no unresolved values, no entry
carries a raw choice expression, `LICENCE_DECISION.md` names every
blocking finding, the notice contains the ten markers and the two
routes, and the venture's own tests pass, because the waitlist still
had to work. The judgement calls, whether the disposition was right and
whether the lawful basis is correct, are flagged for a human and are
listed as such in `packs/legal-licensing/CHECKS.md`.

The run took two passes over the tree and one after the substitution,
inside the budget in D8, and the elapsed time went into the record next
to the decisions.

## What would have gone wrong without the pack

A policy written around distribution reads the tree as clean, because
nothing is distributed. The vendored directory reads as an unknown to
resolve later rather than as a refusal. The choice expression is copied
into the inventory and looks like an answer. The scan runs, reports
nothing actionable, and is treated as a pass. The waitlist collects
addresses with no notice and no registration.

Every one of those is a failure mode listed in the pack, and every one
of them looks like a clean run at the time.
